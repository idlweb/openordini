from open_municipio.om.views import HomeView
from open_municipio.acts.models import Act
from open_municipio.newscache.models import News
from ..commons.mixins import FilterActsByUser, FilterNewsByUser

class OOHomeView(FilterActsByUser, FilterNewsByUser, HomeView):

    def get_context_data(self, **kwargs):

        ctx = super(OOHomeView, self).get_context_data(**kwargs)

        last_presented_acts = Act.objects.filter(presentation_date__isnull=False).distinct()
        filtered_presented_acts = self.filter_acts(last_presented_acts, self.request.user).order_by('-presentation_date')[0:3]
        ctx["last_presented_acts"] = filtered_presented_acts

        # filter community news about private acts

        all_news = News.objects.filter(news_type=News.NEWS_TYPE.community, priority=1).exclude()
        filtered_news = self.filter_news(all_news, self.request.user)
        ctx['last_community_news'] = sorted(filtered_news, key=lambda n: n.news_date, reverse=True)[0:3]

        return ctx


