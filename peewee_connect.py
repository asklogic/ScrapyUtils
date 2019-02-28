import peewee

# db = peewee.MySQLDatabase('scjst', user='root', password='87886700', host='123.207.56.193', port=3306,
#                           charset='utf8mb4')
db = peewee.MySQLDatabase('corporate-information', user='root', password='Aa-123456', host='39.98.41.178', port=3306,
                          charset='utf8mb4')

db1 = peewee.MySQLDatabase('scjst', user='root', password='878867', host='123.207.56.193', port=3306,
                           charset='utf8mb4')


class EnterpriseSimple(peewee.Model):
    UID = peewee.PrimaryKeyField()

    location = peewee.CharField(null=True)
    title = peewee.CharField(null=True, unique=True)
    url = peewee.CharField(null=False)
    code = peewee.CharField(null=True)
    representative = peewee.CharField(null=True)

    class Meta:
        table_name = "origin_enterprise_simple"


class EnterpriseDetail(peewee.Model):
    UID = peewee.PrimaryKeyField()

    dd_id = peewee.TextField()
    origin_json = peewee.TextField()

    class Meta:
        table_name = "origin_enterprise_detail"


class PersonSimple(peewee.Model):
    UID = peewee.PrimaryKeyField()

    location = peewee.CharField(null=True)
    name = peewee.CharField(null=True)
    url = peewee.CharField(null=False)
    code = peewee.CharField(null=True)

    # representative = peewee.CharField(null=True)

    class Meta:
        table_name = "origin_person_simple"


class PersonDetail(peewee.Model):
    UID = peewee.PrimaryKeyField()

    dd_id = peewee.TextField()
    origin_json = peewee.TextField()

    class Meta:
        table_name = "origin_person_detail"


class ProjectSimple(peewee.Model):
    UID = peewee.PrimaryKeyField()

    location = peewee.CharField(null=True)
    title = peewee.CharField(null=True, unique=True)
    url = peewee.CharField(null=False)
    code = peewee.CharField(null=True)
    date = peewee.DateField(null=True)

    class Meta:
        table_name = "origin_project_simple"


class ProjectDetail(peewee.Model):
    UID = peewee.PrimaryKeyField()

    dd_id = peewee.TextField()
    origin_json = peewee.TextField()

    class Meta:
        table_name = "origin_project_detail"


EnterpriseSimple.bind(db1)
EnterpriseDetail.bind(db1)
PersonSimple.bind(db1)
PersonDetail.bind(db1)
ProjectSimple.bind(db1)
ProjectDetail.bind(db1)

EnterpriseSimple.create_table()
EnterpriseDetail.create_table()
PersonSimple.create_table()
PersonDetail.create_table()
ProjectSimple.create_table()
ProjectDetail.create_table()


# class ProjectSimple(peewee.Model):
#     UID = peewee.PrimaryKeyField()
#
#     location = peewee.CharField(null=True)
#     title = peewee.CharField(null=True)
#     url = peewee.CharField(null=False, unique=True)
#     # url = peewee.CharField(null=False)
#     code = peewee.CharField(null=True)
#     date = peewee.DateField(null=True)
#
#     class Meta:
#         table_name = "sys_project_simple"
#
#
# class ProjectDetail(peewee.Model):
#     UID = peewee.PrimaryKeyField()
#
#     dd_id = peewee.CharField(null=True)
#     # name
#     projectName = peewee.CharField(null=True)
#     # address
#     address = peewee.CharField(null=True)
#     # reference_num
#     projectNumber = peewee.CharField(null=True)
#     # attribution
#     xmsdmc = peewee.CharField(null=True)
#     # type1 & type2
#     projectItemType = peewee.CharField(null=True)
#     # usage
#     projectLevel = peewee.CharField(null=True)
#     # investment
#     cost = peewee.CharField(null=True)
#     # code
#     bh = peewee.CharField(null=True)
#
#     class Meta:
#         table_name = "sys_project_detail"


class ProjectBidding(peewee.Model):
    id = peewee.PrimaryKeyField()

    dd_id = peewee.TextField()
    unit_name = peewee.TextField()
    unit_grade = peewee.TextField()
    notice_code = peewee.TextField()
    amount = peewee.TextField()
    bid_date = peewee.TextField()
    detail_id = peewee.TextField()
    parent_id = peewee.TextField()

    class Meta:
        table_name = "sys_pro_bidding"


class ProjectBidDetail(peewee.Model):
    id = peewee.PrimaryKeyField()

    dd_id = peewee.TextField()
    detail_id = peewee.TextField()

    unit_name = peewee.TextField()
    unit_id = peewee.TextField()
    notice_code = peewee.TextField()
    amount = peewee.TextField()
    bid_date = peewee.TextField()
    reference_num = peewee.TextField()
    pro_name = peewee.TextField()
    pro_code = peewee.TextField()
    build_unit = peewee.TextField()
    type2 = peewee.TextField()
    pro_address = peewee.TextField()
    investment = peewee.TextField()
    build_scale = peewee.TextField()
    build_nature = peewee.TextField()
    usage = peewee.TextField()
    tender_type = peewee.TextField()
    tender_mode = peewee.TextField()
    record_date = peewee.TextField()
    pro_id = peewee.TextField()

    class Meta:
        table_name = "sys_pro_bid_detail"


class ProjectConDraEntity(peewee.Model):
    id = peewee.PrimaryKeyField()

    dd_id = peewee.TextField()
    role = peewee.TextField()
    ent_name = peewee.TextField()
    ent_id = peewee.TextField()
    qualification = peewee.TextField()
    distrrict = peewee.TextField()
    detail_id = peewee.TextField()

    class Meta:
        table_name = "sys_pro_con_dra_entity"


class ProjectConDraDetail(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    pro_name = peewee.TextField()
    pro_code = peewee.TextField()
    build_unit = peewee.TextField()
    type2 = peewee.TextField()
    pro_address = peewee.TextField()
    investment = peewee.TextField()
    build_scale = peewee.TextField()
    build_nature = peewee.TextField()
    usage = peewee.TextField()
    detail_id = peewee.TextField()
    notice_code = peewee.TextField()
    qualified_code = peewee.TextField()
    complete_date = peewee.TextField()

    class Meta:
        table_name = "sys_pro_con_dra_detail"


class ProjectContract(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    contract_type = peewee.TextField()
    contract_contract_code = peewee.TextField()
    contract_amount = peewee.TextField()
    contract_date = peewee.TextField()
    detail_id = peewee.TextField()
    parent_id = peewee.TextField()

    class Meta:
        table_name = "sys_pro_contract"


class ProjectContractDetail(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()

    pro_name = peewee.TextField()
    pro_code = peewee.TextField()
    build_unit = peewee.TextField()
    type2 = peewee.TextField()
    pro_address = peewee.TextField()
    investment = peewee.TextField()
    build_scale = peewee.TextField()
    build_nature = peewee.TextField()
    usage = peewee.TextField()
    owner_unit = peewee.TextField()
    owner_unit_id = peewee.TextField()
    job_unit = peewee.TextField()
    job_unit_id = peewee.TextField()
    contract_code = peewee.TextField()
    joint_job_unit = peewee.TextField()
    contract_type = peewee.TextField()
    contract_contract_code = peewee.TextField()
    contract_amount = peewee.TextField()
    contract_date = peewee.TextField()

    class Meta:
        table_name = "sys_pro_contract_detail"


class ProjectPermit(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()

    permit_code = peewee.TextField()
    unit_pro = peewee.TextField()
    contract_amount = peewee.TextField()
    build_scale = peewee.TextField()
    permit_unit = peewee.TextField()
    detail_id = peewee.TextField()

    class Meta:
        table_name = "sys_pro_permit"


ProjectPermit.bind(db)
ProjectPermit.create_table()


class ProjectPermitEntity(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()

    role = peewee.TextField()
    ent_name = peewee.TextField()
    ent_id = peewee.TextField()
    qualification = peewee.TextField()
    detail_id = peewee.TextField()

    class Meta:
        table_name = "sys_pro_permit_entity"


class ProjectPermitDetail(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()

    permit_code = peewee.TextField()
    unit_pro = peewee.TextField()
    contract_amount = peewee.TextField()
    build_scale = peewee.TextField()
    permit_unit = peewee.TextField()

    permit_date = peewee.TextField()
    pro_name = peewee.TextField()
    pro_code = peewee.TextField()
    build_unit = peewee.TextField()
    investment = peewee.TextField()
    pro_address = peewee.TextField()
    safety_permit_code = peewee.TextField()
    contract_contract_code = peewee.TextField()
    qualified_code = peewee.TextField()
    project_manager = peewee.TextField()
    chief_engineer = peewee.TextField()
    quality_supervision = peewee.TextField()
    safety_supervision = peewee.TextField()

    class Meta:
        table_name = "sys_pro_permit_detail"


class ProjectAcceptance(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()
    parent_id = peewee.TextField()

    acceptance_code = peewee.TextField()
    cost_total = peewee.TextField()
    actual_build_scale = peewee.TextField()
    actual_start_date = peewee.TextField()
    actual_completion_date = peewee.TextField()

    class Meta:
        table_name = "sys_pro_acceptance"


class ProjectAcceptanceDetail(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()

    pro_name = peewee.TextField()
    pro_code = peewee.TextField()
    reference_num = peewee.TextField()
    build_unit = peewee.TextField()
    type2 = peewee.TextField()
    pro_address = peewee.TextField()
    investment = peewee.TextField()
    build_scale = peewee.TextField()
    build_nature = peewee.TextField()
    usage = peewee.TextField()

    cost_total = peewee.TextField()
    actual_build_scale = peewee.TextField()
    actual_start_date = peewee.TextField()
    actual_completion_date = peewee.TextField()
    acceptance_code = peewee.TextField()
    completion_date = peewee.TextField()

    class Meta:
        table_name = "sys_pro_acceptance_detail"


class ProjectAcceptanceEntity(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()

    unit_name = peewee.TextField()
    ent_name = peewee.TextField()
    qualification = peewee.TextField()
    qualification_code = peewee.TextField()

    class Meta:
        table_name = "sys_pro_acceptance_entity"


class ProjectAcceptancePersonnel(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()

    role = peewee.TextField()
    ent_id = peewee.TextField()
    ent_id_name = peewee.TextField()
    per_certificate = peewee.TextField()
    name = peewee.TextField()
    name_id = peewee.TextField()
    per_certificate_code = peewee.TextField()

    class Meta:
        table_name = "sys_pro_acceptance_personnel"


class ProjectEntity(peewee.Model):
    id = peewee.PrimaryKeyField()
    detail_id = peewee.TextField()
    parent_id = peewee.TextField()
    dd_id = peewee.TextField()

    pro_id = peewee.TextField()
    pro_name = peewee.TextField()
    unit_role = peewee.TextField()
    ent_id = peewee.TextField()
    ent_name = peewee.TextField()
    total_code = peewee.TextField()

    class Meta:
        table_name = "sys_pro_entity"


class ProjectEntityDetail(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()
    pro_name = peewee.TextField()
    ent_name = peewee.TextField()

    class Meta:
        table_name = "sys_pro_entity_detail"


class ProjectEntityPerson(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()

    role = peewee.TextField()
    pro_name = peewee.TextField()
    per_id = peewee.TextField()
    certificate_code = peewee.TextField()
    position = peewee.TextField()
    job_title = peewee.TextField()
    course = peewee.TextField()
    register_course = peewee.TextField()

    class Meta:
        table_name = "sys_pro_entity_person"


class ProjectEntityEnterprise(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()

    dwgc = peewee.TextField()
    total_code = peewee.TextField()
    build_unit = peewee.TextField()
    unit_address = peewee.TextField()
    ent_name = peewee.TextField()
    build_type = peewee.TextField()

    class Meta:
        table_name = "sys_pro_entity_ent"


class ProjectEntityCertificate(peewee.Model):
    id = peewee.PrimaryKeyField()
    dd_id = peewee.TextField()
    detail_id = peewee.TextField()
    certificate_code = peewee.TextField()
    qualification = peewee.TextField()

    class Meta:
        table_name = "sys_pro_entity_certificate"


# ProjectSimple.bind(db)
# ProjectDetail.bind(db)

ProjectBidding.bind(db)
ProjectBidDetail.bind(db)
ProjectConDraDetail.bind(db)
ProjectConDraEntity.bind(db)
ProjectContract.bind(db)
ProjectContractDetail.bind(db)
ProjectPermitEntity.bind(db)
ProjectPermitDetail.bind(db)

ProjectAcceptance.bind(db)
ProjectAcceptanceDetail.bind(db)
ProjectAcceptanceEntity.bind(db)
ProjectAcceptancePersonnel.bind(db)

ProjectEntity.bind(db)
ProjectEntityCertificate.bind(db)
ProjectEntityDetail.bind(db)
ProjectEntityPerson.bind(db)
ProjectEntityEnterprise.bind(db)


class EnterpriseSimple(peewee.Model):
    id = peewee.PrimaryKeyField()


# ProjectSimple.drop_table()
ProjectSimple.create_table()

if __name__ == '__main__':
    print("yeah!")

    # res = ProjectDetail.select(ProjectDetail.dd_id, ProjectDetail.bh).where(
    #     (ProjectDetail.UID > 0) & (ProjectDetail.UID < 500))
    # print(res[0].bh)

    pass
