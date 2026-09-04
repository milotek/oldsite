{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (p: [
      p.markdown
      p.pyyaml
      p.pillow
      p.fonttools
      p.brotli
    ]))
  ];
}
