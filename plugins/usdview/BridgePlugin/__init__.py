from pxr.Usdviewq.plugin import PluginContainer

def _start_bridge(usdviewApi):
    import os, sys
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    tools = os.path.join(repo, "tools")
    if tools not in sys.path: sys.path.insert(0, tools)
    import usdview_bridge
    if hasattr(usdview_bridge, "start_server"):
        usdview_bridge.start_server(usdviewApi)
    else:
        usdview_bridge.serve(usdviewApi.stage, usdviewApi)

class BridgePluginContainer(PluginContainer):
    def registerPlugins(self, plugRegistry, usdviewApi):
        plugRegistry.registerCommandPlugin(
            "BridgePluginContainer.startBridge",
            "Start JSON Bridge",
            _start_bridge
        )
    def configureView(self, plugRegistry, plugUIBuilder):
        _start_bridge(plugUIBuilder.usdviewApi)

