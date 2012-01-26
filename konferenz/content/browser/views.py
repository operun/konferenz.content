from Acquisition import aq_inner
from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from konferenz.content.interfaces import ITalk

class TalkView(BrowserView):
    
    __call__ = ViewPageTemplateFile('templates/talk.pt')
    
class TalkFolderView(BrowserView):

    __call__ = ViewPageTemplateFile('templates/talkfolder.pt')


class TalkListingView(BrowserView):

    __call__ = ViewPageTemplateFile('templates/talklisting.pt')

    def _query(self):
        """ get all talks
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        results = catalog(portal_type='Talk', sort_on='sortable_title')
        
        return results
    

    def talks(self):
        """ return talks
        """
        talks = self._query()
        
        return talks