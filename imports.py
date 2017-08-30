def find_env_root():
    """Recursively search for `environment.yml`."""
    import os
    root = '.'
    for i in range(4):
        if os.path.isfile(os.path.join(root, 'environment.yml')):
            return root
        root = os.path.join(root, '..')
    raise IOError('Could not find `environment.yml`.')


def import_stdlibs():
    """Import common standard library packages."""
    import importlib
    libs = [
        'collections',
        'datetime',
        'functools',
        'glob',
        'gzip',
        'io',
        'itertools',
        'json',
        'logging',
        'math',
        'os',
        'random',
        're',
        'shutil',
        'subprocess',
        'sys',
        'tempfile',
        'time',
        'urllib',
        'zipfile'
    ]
    for lib in libs:
        globals()[lib] = importlib.import_module(lib)


def import_condalibs():
    """Import packages listed in `environment.yml`."""
    import importlib
    import os
    import re
    dependency_exceptions = {
        'pandas': 'numpy',  # Recommended: numexpr, bottleneck
        'scikit-learn': ('numpy', 'scipy'),
        'seaborn': 'matplotlib'
    }
    import_exceptions = {
        'beautifulsoup4': ('bs4', 'bs4'),
        'numpy': 'np',
        'pandas': 'pd',
        'py-xgboost': ('xgb', 'xgboost'),
        'scikit-learn': ('sklearn', 'sklearn'),
        'seaborn': 'sns',
        'xgboost': 'xgb'
    }
    # Read `environment.yml`.
    root = find_env_root()
    with open(os.path.join(root, 'environment.yml')) as f:
        env = '\n'.join(f.readlines())
    # Extract all conda packages from the environment file.
    pkgs = list(re.findall(r'\s+-\s+([0-9a-z-]+)', env))
    # Add implicit dependencies.
    # Even better would be to list explicit dependencies in `environment.yml`.
    for pkg in dependency_exceptions:
        if pkg in pkgs:
            deps = dependency_exceptions[pkg]
            if isinstance(deps, str):
                deps = (deps,)
            for dep in deps:
                if dep not in pkgs:
                    pkgs.append(dep)
    # Import packages.
    for pkg in pkgs:
        # Handle special cases.
        if pkg in import_exceptions:
            if isinstance(import_exceptions[pkg], str):
                name, mod = import_exceptions[pkg], pkg
            else:
                name, mod = import_exceptions[pkg]
        else:
            name, mod = pkg, pkg
        # Import package.
        try:
            globals()[name] = importlib.import_module(mod)
        except:
            pass
        # Import extras.
        if mod == 'line_profiler':
            from IPython import get_ipython
            get_ipython().run_line_magic('load_ext', 'line_profiler')
        if mod == 'memory_profiler':
            from IPython import get_ipython
            get_ipython().run_line_magic('load_ext', 'memory_profiler')
        if mod == 'pandas':
            # It should be up to the user to limit the DataFrame output.
            pd = globals()['pd']
            pd.options.display.max_columns = 500
            pd.options.display.max_rows = 500
        if mod == 'matplotlib':
            globals()['plt'] = importlib.import_module('matplotlib.pyplot')
            # Use a better default style.
            plt = globals()['plt']
            plt.style.use('seaborn-whitegrid')
            # Inline and retina-quality plots.
            from IPython import get_ipython
            get_ipython().run_line_magic('matplotlib', 'notebook')
            get_ipython().run_line_magic(
                'config', "InlineBackend.figure_format = 'retina'")
            # Fix inconsistent DPIs (see matplotlib #4853).
            plt.rcParams['savefig.dpi'] = plt.rcParams['figure.dpi']
            # Better default figure size.
            plt.rcParams['figure.figsize'] = 9.5, 9.5 / (16 / 9)
            # Better default figure margins.
            plt.rcParams['figure.autolayout'] = True
            # Better default font families (with fallback).
            # Run `font_manager._rebuild()` to rebuild the font cache.
            plt.rcParams['font.sans-serif'].insert(0, 'Roboto')
            plt.rcParams['font.monospace'].insert(0, 'Roboto Mono')
        if mod == 'plotly':
            globals()['py'] = importlib.import_module('plotly.offline')
            globals()['go'] = importlib.import_module('plotly.graph_objs')
            globals()['tls'] = importlib.import_module('plotly.tools')
            py = globals()['py']
            py.init_notebook_mode(connected=False)


def import_locallibs():
    """Import local packages."""
    import importlib
    import os
    import sys
    root = find_env_root()
    toplevels = [
        root,
        os.path.join(root, 'src'),
        os.path.join(root, 'source')
    ]
    for top in toplevels:
        if os.path.isdir(top):
            sys.path.append(top)
            for mod in os.listdir(top):
                if mod[0] != '.' and os.path.isdir(os.path.join(top, mod)):
                    globals()[mod] = importlib.import_module(mod)


def display_all_variables():
    """Display all evaluated variables in a cell."""
    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = 'all'


def autoreload_modules():
    """Enable autoreloading."""
    from IPython import get_ipython
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')


if __name__ == '__main__':
    import_stdlibs()
    import_condalibs()
    import_locallibs()
    display_all_variables()
    autoreload_modules()
