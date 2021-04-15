{ pkgs ? import <nixpkgs> {} }:

pkgs.python3Packages.buildPythonApplication {
  pname = "Coniunctum";
  src = ./.;
  version = "0.2";
  propagatedBuildInputs = [ 
      pkgs.python3
      pkgs.python3Packages.pyperclip ];
}