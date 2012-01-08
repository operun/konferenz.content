from Acquisition import aq_inner
from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from konferenz.content.interfaces import ITalk

class TalkView(BrowserView):
    
    __call__ = ViewPageTemplateFile('talk.pt')
    
class TalkFolderView(BrowserView):

    __call__ = ViewPageTemplateFile('talkfolder.pt')
