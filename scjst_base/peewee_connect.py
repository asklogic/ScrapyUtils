import peewee

db = peewee.MySQLDatabase('scjst', user='root', password='87886700', host='logic-ol.me', port=3306,
                          charset='utf8mb4')


class ProjectBase(peewee.Model):
    UID = peewee.PrimaryKeyField()

    location = peewee.CharField(null=True)
    title = peewee.CharField(null=True)
    url = peewee.CharField(null=False, unique=True)
    # url = peewee.CharField(null=False)
    code = peewee.CharField(null=True)
    date = peewee.DateField(null=True)

    class Meta:
        table_name = "Project_Base"


ProjectBase.bind(db)
# ProjectBase.drop_table()
ProjectBase.create_table()





if __name__ == '__main__':
    pass

# urls = []
# for url in urls:
#     if urls.count(url) > 1:
#         print("wat")
