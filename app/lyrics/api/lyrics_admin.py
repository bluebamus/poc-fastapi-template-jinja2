from sqladmin import ModelView

from app.lyrics.models import (  # noqa: F401
    Attribute,
    PromptTemplate,
    SongResultsAll,
    SongSample,
    StoreDefaultInfo,
)


class LyricsStoreDefaultInfoAdmin(ModelView, model=StoreDefaultInfo):
    name = "상가 기본 정보"
    name_plural = "상가 정보 목록"
    icon = "fa-solid fa-store"
    category = "상가 정보 관리"
    page_size = 20

    column_list = ["id", "store_name"]

    # 폼(생성/수정)에서 제외
    form_excluded_columns = ["created_at"]

    column_searchable_list = [
        StoreDefaultInfo.store_name,
        StoreDefaultInfo.store_phone_number,
    ]

    column_default_sort = (StoreDefaultInfo.store_name, False)  # False: ASC, True: DESC

    column_sortable_list = [
        StoreDefaultInfo.created_at,
        StoreDefaultInfo.store_phone_number,
    ]

    # 폼 컬럼 (기존 유지, user_posts가 관계라면 모델에 정의 필요)
    # form_columns = [
    #     Post.user_id,
    #     Post.title,
    #     Post.content,
    #     Post.is_published,
    #     Post.user_posts,  # Many-to-Many 또는 One-to-Many 관계 가정
    # ]


class LyricsAttributeAdmin(ModelView, model=Attribute):
    name = "속성"
    name_plural = "속성 목록"
    icon = "fa-solid fa-tags"
    category = "속성 관리"
    page_size = 20

    column_list = ["id", "attr_category"]

    # 폼(생성/수정)에서 제외
    form_excluded_columns = ["created_at"]

    column_searchable_list = [
        Attribute.attr_category,
        Attribute.attr_value,
    ]

    column_default_sort = (Attribute.created_at, False)  # False: ASC, True: DESC

    column_sortable_list = [
        Attribute.created_at,
    ]


class LyricsSongSampleAdmin(ModelView, model=SongSample):
    name = "가사 샘플"
    name_plural = "가사 샘플 목록"
    icon = "fa-solid fa-flask"
    category = "가사 샘플 관리"
    page_size = 20

    column_list = [
        "id",
        "ai_model",
        "season",
        "num_of_people",
        "people_category",
        "genre",
    ]

    # 폼(생성/수정)에서 제외
    form_excluded_columns = ["created_at"]

    column_default_sort = (SongSample.created_at, False)  # False: ASC, True: DESC


class LyricsPromptTemplateAdmin(ModelView, model=PromptTemplate):
    name = "프롬프트 템플릿"
    name_plural = "프롬프트 템플릿 목록"
    icon = "fa-solid fa-file-alt"
    category = "프롬프트 템플릿 관리"
    page_size = 20

    column_list = [
        "id",
        "description",
    ]

    # 폼(생성/수정)에서 제외
    form_excluded_columns = ["created_at"]

    column_default_sort = (PromptTemplate.created_at, False)  # False: ASC, True: DESC


class LyricsSongResultsAllAdmin(ModelView, model=SongResultsAll):
    name = "가사 결과"
    name_plural = "가사 결과 목록"
    icon = "fa-solid fa-music"
    category = "가사 결과 관리"
    page_size = 20

    column_list = [
        "id",
        "store_name",
    ]

    # 폼(생성/수정)에서 제외
    form_excluded_columns = ["created_at"]

    column_searchable_list = [
        SongResultsAll.ai,
        SongResultsAll.ai_model,
    ]

    column_default_sort = (SongResultsAll.created_at, False)  # False: ASC, True: DESC

    column_sortable_list = [
        SongResultsAll.store_name,
        SongResultsAll.store_category,
        SongResultsAll.ai,
        SongResultsAll.ai_model,
        SongResultsAll.num_of_people,
        SongResultsAll.genre,
        SongResultsAll.created_at,
    ]
