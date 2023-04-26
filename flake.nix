{
  outputs = { self, nixpkgs }:
    let forAllSystems = nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed;
    in {
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          pythonPkgs = ps: with ps; [ requests ];
        in
        {
          default = (pkgs.python3.withPackages pythonPkgs).env;
        }
      );
    };
}
