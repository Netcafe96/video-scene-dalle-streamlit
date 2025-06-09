{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.ffmpeg
    pkgs.cairo
    pkgs.pkg-config
    pkgs.libGL
  ];
}
