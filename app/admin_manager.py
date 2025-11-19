# from fastapi import FastAPI
# from sqladmin import Admin

# from app.database.session import engine
# from app.home.home_admin import PostAdmin
# from app.lyrics.lyrics_admin import GroupAdmin, UserAdmin, UserProfileAdmin
# from config import ProjectSettings

# # from app.api.v1.routers.celery.celery_admin import (
# #     CeleryTaskAdmin,
# #     CeleryBeatIntervalScheduleAdmin,
# #     CeleryBeatClockedScheduleAdmin,
# #     CeleryBeatCrontabScheduleAdmin,
# #     CeleryBeatSolarScheduleAdmin,
# #     CeleryBeatPeriodicTaskChangedEventAdmin,
# #     CeleryBeatPeriodicTaskAdmin,
# # )

# # https://github.com/aminalaee/sqladmin


# def init_admin(
#     app: FastAPI,
#     db_engine: engine,
#     base_url: str = ProjectSettings.ADMIN_BASE_URL,
# ) -> Admin:
#     admin = Admin(
#         app,
#         db_engine,
#         base_url=base_url,
#     )

#     admin.add_view(UserAdmin)
#     admin.add_view(UserProfileAdmin)
#     admin.add_view(GroupAdmin)
#     admin.add_view(PostAdmin)
#     # admin.add_view(CeleryTaskAdmin)
#     # admin.add_view(CeleryBeatIntervalScheduleAdmin)
#     # admin.add_view(CeleryBeatClockedScheduleAdmin)
#     # admin.add_view(CeleryBeatCrontabScheduleAdmin)
#     # admin.add_view(CeleryBeatSolarScheduleAdmin)
#     # admin.add_view(CeleryBeatPeriodicTaskChangedEventAdmin)
#     # admin.add_view(CeleryBeatPeriodicTaskAdmin)

#     return admin
