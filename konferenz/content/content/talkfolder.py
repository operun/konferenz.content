from zope.interface import implements
from zope.component import adapts

from Products.Archetypes.atapi import *

from Products.Archetypes.interfaces import IObjectPostValidation

from Products.validation import V_REQUIRED

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from konferenz.content.interfaces import ITalkFolder
from konferenz.content.config import PROJECTNAME

from konferenz.content import KonferenzContentMessageFactory as _

schema = Schema((

    TextField('text',
        required=False,
        searchable=True,
        storage=AnnotationStorage(),
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        widget=RichWidget(label=_(u"Body Text"),
                          description=_(u""),
                          rows=25,
                          allow_file_upload=False)   
        ),
    ))

TalkFolderSchema = ATFolderSchema.copy() + schema.copy()

TalkFolderSchema['title'].storage = AnnotationStorage()
TalkFolderSchema['description'].storage = AnnotationStorage()

finalizeATCTSchema(TalkFolderSchema, folderish=True, moveDiscussion=False)

class TalkFolder(ATFolder):
    """Talk Folder
    """

    implements(ITalkFolder)

    portal_type = "Talk Folder"
    _at_rename_after_creation = True

    schema = TalkFolderSchema
    
    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    text = ATFieldProperty('text')
    
registerType(TalkFolder, PROJECTNAME)
