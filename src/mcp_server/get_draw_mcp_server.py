import subprocess
from pathlib import Path

from fastmcp import FastMCP


def get_draw_mcp_server(target_dir: str, host: str, port: int) -> FastMCP:
    mcp = FastMCP("draw_mcp_server")

    @mcp.tool()
    def draw_puml(puml_code: str, filename: str) -> str:
        """Draws a diagram from the given PUML code using PlantUML.

        This tool receives PUML code and generates a diagram using PlantUML.
        It returns a URL referencing the generated diagram.

        Parameters
        ----------
        puml_code : str
            The PlantUML code to be rendered into a diagram.
        filename : str.
            Saved file name (example: image.png)

        Returns
        -------
        str
            A URL referencing the generated diagram.

        """
        try:
            # Ensure target directory exists
            target_path = Path(target_dir)
            target_path.mkdir(parents=True, exist_ok=True)

            # Write PUML code to file (add handler option if missing)
            # Some PlantUML versions do not support "!option handler", so use "!pragma handler" instead
            if "!pragma handler" not in puml_code:
                puml_code = "!pragma handler local\n" + puml_code

            puml_file = target_path / f"{(Path(filename).stem)}.puml"
            puml_file.write_text(puml_code, encoding="utf-8")

            # Execute PlantUML command to generate diagram
            subprocess.run(["plantuml", str(puml_file)], check=True)  # noqa: S603, S607
        except Exception as e:  # noqa: BLE001
            return f"Diagram generation failed due to an unexpected error: {e}"
        else:
            # Return the URL to access the generated diagram
            return f"http://{host}:{port}/api/v1/data/{filename}"

    return mcp
