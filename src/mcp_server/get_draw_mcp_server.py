from fastmcp import FastMCP


def get_draw_mcp_server(host: str, port: int) -> FastMCP:
    mcp = FastMCP("draw_mcp_server")

    @mcp.tool()
    def draw_puml(puml_code: str) -> str:
        """Draws a diagram from the given PUML code using PlantUML.

        This tool receives PUML code and generates a diagram using PlantUML.
        It returns a URL referencing the generated diagram.

        Parameters
        ----------
        puml_code : str
            The PlantUML code to be rendered into a diagram.

        Returns
        -------
        str
            A URL referencing the generated diagram.

        """
        return ""

    return mcp
