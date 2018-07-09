from flask_table import Table, Col,LinkCol

class Results(Table):
    id = Col('Id', show =False)
    cat = Col('Cat')
    name = Col('Name')
    edit = LinkCol('Edit', 'edit', url_kwargs = dict(id='id'))
    delete = LinkCol('Delete', 'remove', url_kwargs = dict(id = 'id'))

class Water(Table):
    id = Col('Id', show = False)
    name = Col ('Name')
    customer = Col('Customer')
    engineering = Col('Engineering')
    extra = Col('Extra')
    edit = LinkCol('Edit', 'change', url_kwargs = dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs = dict(id = 'id'))
