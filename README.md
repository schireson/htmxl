## Schireson Excel

[Docs!](http://docs.schireson.com/packages/schireson-excel/latest/)

### Hello World


    from schireson_excel.compose import Workbook

    workbook = Workbook()
    workbook.add_sheet_from_template(
        template="""<head>{{ title }}</head>  # This defines the worksheet name
        <body><div>Hello down there, {{ bottom_name }}!</div><br><div>Hello up there, {{ top_name }}!</div>
        """,
        data={
            title="Hello World",
            top_name='two rows up',
            bottom_name='two rows down',
        }

    )

    workbook.compose('hello_world.xlsx')
