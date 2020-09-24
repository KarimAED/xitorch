import inspect

def get_methods_docstr(cls_or_func, methods, ignore_kwargs=None):
    """
    Get the full docstring of a class or a function. Full docstring is the
    main docstring of the class or function plus docstrings of the methods
    (usually to describe the options available specifically for a specific
    method).

    Arguments
    ---------
    * cls_or_func: class or callable
        Main class or function
    * methods: list or dict
        If a list, it lists the methods with the same method name options.
        If a dict, it contains the method name as the keys and the method
        function or class as the value.
    * ignore_kwargs: list or None
        List of string on which kwargs to be ignored in addition to ["params"]

    Returns
    -------
    * full_docstr: str
        The full docstring of cls_or_func
    """
    method_template = """
    Methods
    -------
    ({kwargs_sig})
    """
    res = cls_or_func.__doc__

    def_ignore_kwargs = ["params"]
    if ignore_kwargs is None:
        ignore_kwargs = []
    ignore_kwargs = ignore_kwargs + def_ignore_kwargs

    if isinstance(methods, dict):
        generator = methods.items()
    elif isinstance(methods, list):
        generator = ((method.__name__, method) for method in methods)
    else:
        raise TypeError("methods must be a list or a dict")

    for name, method in generator:
        # get the signatures
        sigparams = inspect.signature(method).parameters
        kwargs_sig_list = ['method="%s"'%name] + \
            ["%s=%s"%(name,val) for name,val in _get_default_parameters(sigparams, ignore_kwargs)]
        kwargs_sig = ", ".join(kwargs_sig_list)

        # add the method name
        methoddoc = method.__doc__
        res = res + method_template.format(
            kwargs_sig=kwargs_sig,
        )
        if methoddoc is not None:
            method_doc = _add_indent(method.__doc__, " "*4)
            res = res + method_doc
    return res

def _get_default_parameters(parameters, ignore_kwargs):
    empty = inspect.Parameter.empty
    for paramname in parameters:
        if paramname in ignore_kwargs:
            continue
        defval = parameters[paramname].default
        if defval == empty:
            continue
        defval = defval if not isinstance(defval, str) else '"%s"'%defval
        yield paramname, defval

def _add_indent(s, indent):
    return "\n".join([indent+line for line in s.split("\n")])
