{
  inputs = {
    # this is equivalent to `nixpkgs = { url = "..."; };`
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  # now a set 👇
  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default =
          with pkgs;
          mkShell {
            buildInputs = [
              (pkgs.python3.withPackages (
                python-pkgs: with python-pkgs; [
                  python-multipart # ???????
                  requests
                  pydantic
                  fastapi
                  pyjwt
                  passlib
                  sqlmodel
                  pytest
                ]
              ))
            ];
          };
      }
    );
}
