from routers.utils.page_static import cut_selector


def test_cut_selector():
    selector = "html > body.wp-manga-template-default.single.single-wp-manga.postid-3334.wp-embed-responsive.wp-manga" \
               "-page.manga-page.page.header-style-1.sticky-enabled.sticky-style-2.is-sidebar.text-ui-dark.sticky-for" \
               "-mobile > div.wrap > div.body-wrap > div.site-content > " \
               "div.post-3334.wp-manga.type-wp-manga.status-publish.has-post-thumbnail.hentry.wp-manga-release-389.wp" \
               "-manga-author-wilbrite.wp-manga-artist-gabinam.wp-manga-artist-yuahni.wp-manga-genre-action.wp-manga" \
               "-genre-drama.wp-manga-genre-fantasy.wp-manga-genre-historical.wp-manga-genre-isekai.wp-manga-genre" \
               "-romance > div.c-page-content.style-1 > div.content-area > div.container > div.row > " \
               "div.main-col..col-md-8.col-sm-8 > div.main-col-inner > div.c-page > div.c-page__content > " \
               "div.page-content-listing.single-page > div.listing-chapters_wrap.cols-3 > " \
               "ul.main.version-chap.no-volumn "
    assert '..' in selector
    selector = cut_selector(selector)
    assert '..' not in selector
