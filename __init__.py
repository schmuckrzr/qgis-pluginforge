def classFactory(iface):
    """Carga la clase PluginForge desde el archivo plugin_forge.py"""
    from .plugin_forge import PluginForge
    return PluginForge(iface)
