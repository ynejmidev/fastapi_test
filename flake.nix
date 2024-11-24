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
              (pkgs.python3.withPackages (python-pkgs: [
                python-pkgs.fastapi
                python-pkgs.passlib
                python-pkgs.pyjwt
                python-pkgs.requests
                python-pkgs.pydantic
                python-pkgs.python-multipart #???????
              ]))
            ];
          };
      }
    );
}
