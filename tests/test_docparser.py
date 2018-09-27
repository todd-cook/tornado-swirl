from tornado_swirl.docparser import parse_from_docstring, PathSpec

def test_simple_parse_1():
    docstring = """This is the simple description"""

    path_spec = parse_from_docstring(docstring)
    assert isinstance(path_spec, PathSpec)
    assert path_spec.summary == "This is the simple description"


def test_simple_parse_2():
    docstring = """This is the simple description.

    Long description.
    """

    path_spec = parse_from_docstring(docstring)
    assert path_spec.summary == "This is the simple description.\n"
    assert path_spec.description == "Long description.\n"


def test_simple_parse_3():
    docstring = """This is the simple description.
    With a second line.

    Long description.
    With a second line.
    """

    path_spec = parse_from_docstring(docstring)
    assert path_spec.summary == "This is the simple description.\nWith a second line.\n"
    assert path_spec.description == "Long description.\nWith a second line.\n"


def test_simple_parse_4_with_path_params():
    docstring = """This is the simple description.
With a second line.

Long description.
With a second line.

Path Parameters:
    employee_uid (int) -- The employee ID.
"""

    path_spec = parse_from_docstring(docstring)
    assert path_spec.summary == "This is the simple description.\nWith a second line.\n"
    assert path_spec.description == "Long description.\nWith a second line.\n"
    assert path_spec.path_params_section == "    employee_uid (int) -- The employee ID.\n"

    pp = path_spec.path_params.get('employee_uid')
    assert pp.name == 'employee_uid'
    assert pp.type == 'int'
    assert pp.ptype == "path"
    assert pp.description == 'The employee ID.'
    assert pp.required == True


def test_simple_parse_5_with_query_params():
    docstring = """This is the simple description.
With a second line.

Long description.
With a second line.

Query Parameters:
    param1 (int) -- The param 1.
    param2 (Model) -- Required. The param 2.
"""

    path_spec = parse_from_docstring(docstring)
    assert path_spec.summary == "This is the simple description.\nWith a second line.\n"
    assert path_spec.description == "Long description.\nWith a second line.\n"
    assert path_spec.path_params_section == ""
    assert path_spec.query_params_section == "    param1 (int) -- The param 1.\n    param2 (Model) -- Required. The param 2.\n"
    
    qp = path_spec.query_params.get("param1")
    assert qp is not None
    assert qp.name == "param1"
    assert qp.type == "int"
    assert qp.ptype == "query"
    assert qp.required == False
    assert qp.description == "The param 1."

    qp2 = path_spec.query_params.get("param2")
    assert qp2 is not None
    assert qp2.name == "param2"
    assert qp2.type == "Model"
    assert qp2.required
    assert qp2.description == "The param 2."


def test_simple_parse_6_with_body_params():
    docstring = """This is the simple description.
With a second line.

Long description.
With a second line.

Query Parameters:
    param1 (int) -- The param 1.
    param2 (Model) -- Required. The param 2.

Request Body:
    test (Model) -- Required.  This is the bomb.
"""

    path_spec = parse_from_docstring(docstring)
    assert path_spec.summary == "This is the simple description.\nWith a second line.\n"
    assert path_spec.description == "Long description.\nWith a second line.\n"
    assert path_spec.path_params_section == ""
    assert path_spec.query_params_section == "    param1 (int) -- The param 1.\n    param2 (Model) -- Required. The param 2.\n"
    
    qp = path_spec.query_params.get("param1")
    assert qp is not None
    assert qp.name == "param1"
    assert qp.type == "int"
    assert qp.ptype == "query"
    assert qp.required == False
    assert qp.description == "The param 1."

    qp2 = path_spec.query_params.get("param2")
    assert qp2 is not None
    assert qp2.name == "param2"
    assert qp2.type == "Model"
    assert qp2.required
    assert qp2.description == "The param 2."

    body_param = path_spec.body_param
    assert body_param is not None
    assert body_param.name == "test"
    assert body_param.type == "Model"
    assert body_param.required
    assert body_param.description == "This is the bomb."


def test_simple_parse_6_with_body_params_and_headers():
    docstring = """This is the simple description.
With a second line.

Long description.
With a second line.

Headers:
    Authorization -- Required. the login.

Query Parameters:
    param1 (int) -- The param 1.
    param2 (Model) -- Required. The param 2.

Request Body:
    test (Model) -- Required.  This is the bomb.
"""

    path_spec = parse_from_docstring(docstring)
    assert path_spec.summary == "This is the simple description.\nWith a second line.\n"
    assert path_spec.description == "Long description.\nWith a second line.\n"
    assert path_spec.path_params_section == ""
    assert path_spec.query_params_section == "    param1 (int) -- The param 1.\n    param2 (Model) -- Required. The param 2.\n"
    
    qp = path_spec.query_params.get("param1")
    assert qp is not None
    assert qp.name == "param1"
    assert qp.type == "int"
    assert qp.ptype == "query"
    assert qp.required == False
    assert qp.description == "The param 1."

    qp2 = path_spec.query_params.get("param2")
    assert qp2 is not None
    assert qp2.name == "param2"
    assert qp2.type == "Model"
    assert qp2.required
    assert qp2.description == "The param 2."

    body_param = path_spec.body_param
    assert body_param is not None
    assert body_param.name == "test"
    assert body_param.type == "Model"
    assert body_param.required
    assert body_param.description == "This is the bomb."

    hp = path_spec.header_params.get("Authorization")
    assert hp is not None
    assert hp.name == "Authorization"
    assert hp.type == "string"
    assert hp.required 



def test_simple_parse_6_with_body_params_and_headers_array_of_ints():
    docstring = """This is the simple description.
With a second line.

Long description.
With a second line.

Headers:
    Authorization -- Required. the login.

Query Parameters:
    param1 ([int]) -- The param 1.
    param2 (Model) -- Required. The param 2.

Request Body:
    test (Model) -- Required.  This is the bomb.
"""

    path_spec = parse_from_docstring(docstring)
   
    qp = path_spec.query_params.get("param1")
    assert qp is not None
    assert qp.name == "param1"
    assert qp.type == "array"
    assert qp.ptype == "query"
    assert qp.itype == "int"
    assert qp.required == False
    assert qp.description == "The param 1."

    qp2 = path_spec.query_params.get("param2")
    assert qp2 is not None
    assert qp2.name == "param2"
    assert qp2.type == "Model"
    assert qp2.required
    assert qp2.description == "The param 2."

    body_param = path_spec.body_param
    assert body_param is not None
    assert body_param.name == "test"
    assert body_param.type == "Model"
    assert body_param.required
    assert body_param.description == "This is the bomb."

    hp = path_spec.header_params.get("Authorization")
    assert hp is not None
    assert hp.name == "Authorization"
    assert hp.type == "string"
    assert hp.required 


def test_cookie_section():
    docstring = """Cookie Monster

    Cookie:
        x (string) -- required.  Cookie monster raaa
    """
    path_spec = parse_from_docstring(docstring)

    assert path_spec.cookie_params
    cookie = path_spec.cookie_params.get("x")
    assert cookie is not None
    assert cookie.name == 'x'
    assert cookie.type == 'string'
    assert cookie.required
    assert cookie.description == 'Cookie monster raaa'
