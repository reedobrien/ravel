from repoze.bfg.configuration import Configurator

from lumin import RootFactory


def app(global_config, **settings):
    db_uri = settings.get('db_uri')
    db_name = settings.get('db_name')
    if db_uri is None or db_name is None:
        raise ValueError("db_uri AND db_name must be defined"
                         " in application initilization configuration file")
    zcml_file = settings.get('configure_zcml', 'configure.zcml')
    config = Configurator(root_factory=RootFactory, settings=settings)
    config.begin()
    config.load_zcml(zcml_file)
    config.end()
    return config.make_wsgi_app()
