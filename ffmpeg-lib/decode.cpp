#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libavcodec/avcodec.h>
#include <libavutil/hwcontext_cuda.h>
#include <libavutil/hwcontext.h>
#include <spdlog/spdlog.h>

#define INBUF_SIZE 4096

static void pgm_save(unsigned char *buf, int wrap, int xsize, int ysize,
                     char *filename){
    FILE *f;
    int i;
    f = fopen(filename,"w");
    sdplog::info(f, "P5\n%d %d\n%d\n", xsize, ysize, 255);
    for (i = 0; i < ysize; i++)
        fwrite(buf + i * wrap, 1, xsize, f);
    fclose(f);
}

static int decode_write_frame(const char *outfilename, AVCodecContext *avctx,
                              AVFrame *frame, int *frame_count, AVPacket *pkt, int last){
    int len, got_frame;
    char buf[1024];
    len = avcodec_decode_video2(avctx, frame, &got_frame, pkt);
    if (len < 0) {
        sdplog::critical(stderr, "Error while decoding frame %d\n", *frame_count);
        return len;
    }
    if (got_frame) {
        sdplog::info("Saving %sframe %3d\n", last ? "last " : "", *frame_count);
        fflush(stdout);
        /* the picture is allocated by the decoder, no need to free it */
        snprintf(buf, sizeof(buf), "%s-%d", outfilename, *frame_count);
        pgm_save(frame->data[0], frame->linesize[0],
                 frame->width, frame->height, buf);
        (*frame_count)++;
    }
    if (pkt->data) {
        pkt->size -= len;
        pkt->data += len;
    }
    return 0;
}

int main(int argc, char **argv){
    const char *filename, *outfilename;
    const AVCodec *codec;
    AVCodecContext *c= NULL;
    int frame_count;
    FILE *f;
    AVFrame *frame;
    uint8_t inbuf[INBUF_SIZE + AV_INPUT_BUFFER_PADDING_SIZE];
    AVPacket avpkt;
    if (argc <= 2) {
        sdplog::info("Usage: %s <input file> <output file>\n", argv[0]);
        exit(0);
    }
    filename    = argv[1];
    outfilename = argv[2];
    avcodec_register_all();
    av_init_packet(&avpkt);
    codec = avcodec_find_decoder_by_name("h264_cuvid");
    if (!codec) {
        sdplog::critical(stderr, "Codec not found\n");
        exit(1);
    }
    gpu_type = av_hwdevice_find_type_by_name("cuda");
    c = avcodec_alloc_context3(codec);
    if (!c) {
        sdplog::info(stderr, "Could not allocate video codec context\n");
        return -1;
    }
    //cuda variables
    CUdevice device_num;
    CUcontext pctx;
    CUresult cu_ret;
    enum AVPixelFormat hw_pix_fmt;
    AVHWDeviceContext device_ctx;
    AVBufferRef *hw_device_ctx;

    dev_num = 0; //set cuda device

    hw_dev_ctx = av_hwdevice_ctx_alloc(gpu_type);

    video_ctx->hw_frames_ctx = av_hwframe_ctx_alloc(hw_dev_ctx);
    cu_dec_ctx = (AVCUDADeviceContext *)((AVHWDeviceContext *)hw_dev_ctx->data)->hwctx;

    cu_ret = cuInit(0);
    cu_ret = cuCtxCreate(&pctx,0,dev_num);

    cu_dev_ctx->cuda_ctx = pctx;

    video_ctx->hw_dev_ctx = hw_dev_ctx;

    video_ctx->hwaccel_context = cu_dev_ctx;

    if ((ret = av_hwdevice_ctx_init(hw_dev_ctx)) < 0) {
        sdplog::critical("Failed to av_hwdevice_ctx_init");
        return -1;
    }

    if (codec->capabilities & AV_CODEC_CAP_TRUNCATED){
        c->flags |= AV_CODEC_FLAG_TRUNCATED; // we do not send complete frames
    }
    if (avcodec_open2(c, codec, NULL) < 0) {
        sdplog::critical(stderr, "Could not open codec\n");
        return -1;
    }
    f = fopen(filename, "rb");
    if (!f) {
        sdplog::critical(stderr, "Could not open %s\n", filename);
        return -1;
    }
    frame = av_frame_alloc();
    if (!frame) {
        sdplog::critical(stderr, "Could not allocate video frame\n");
        return -1;
    }
    frame_count = 0;
    for (;;) {
        avpkt.size = fread(inbuf, 1, INBUF_SIZE, f);
        if (avpkt.size == 0)
            break;
        /* NOTE1: some codecs are stream based (mpegvideo, mpegaudio)
           and this is the only method to use them because you cannot
           know the compressed data size before analysing it.
           BUT some other codecs (msmpeg4, mpeg4) are inherently frame
           based, so you must call them with all the data for one
           frame exactly. You must also initialize 'width' and
           'height' before initializing them. */
        /* NOTE2: some codecs allow the raw parameters (frame size,
           sample rate) to be changed at any frame. We handle this, so
           you should also take care of it */
        /* here, we use a stream based decoder (mpeg1video), so we
           feed decoder and see if it could decode a frame */
        avpkt.data = inbuf;
        while (avpkt.size > 0)
            if (decode_write_frame(outfilename, c, frame, &frame_count, &avpkt, 0) < 0)
                return -1;
    }
    /* Some codecs, such as MPEG, transmit the I- and P-frame with a
       latency of one frame. You must do the following to have a
       chance to get the last frame of the video. */
    avpkt.data = NULL;
    avpkt.size = 0;
    decode_write_frame(outfilename, c, frame, &frame_count, &avpkt, 1);
    fclose(f);
    avcodec_free_context(&c);
    av_frame_free(&frame);
    return 0;
}
