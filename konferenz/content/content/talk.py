from Products.CMFCore.permissions import View
from AccessControl import ClassSecurityInfo

from zope.interface import implements

try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.atapi import *

from Products.Archetypes.atapi import DisplayList

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.newsitem import ATNewsItem, ATNewsItemSchema

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.validation import V_REQUIRED

from konferenz.content.interfaces import ITalk
from konferenz.content.config import PROJECTNAME

from konferenz.content import KonferenzContentMessageFactory as _

from urllib import quote

LANGUAGE = DisplayList((
    ('ger', _(u'German')),
    ('eng', _(u'English')),
    ))


schema = Schema((

    StringField(
        name='name',
        required=True,
        searchable=True,
        widget=StringField._properties['widget'](
            label='Speaker Name',
            label_msgid='Talk_label_Name',
            i18n_domain='Talk',
        ),
    ),

    TextField(
        name='speaker_info',
        widget=RichWidget(
            label='Speaker Info',
            label_msgid='talk_label_Speaker',
            i18n_domain='talk',
        ),

    ),

    StringField(
        name='company',
        required=True,
        searchable=True,
        widget=StringField._properties['widget'](
            label='Company',
            label_msgid='Talk_label_company',
            i18n_domain='Talk',
        ),
    ),
                 
    StringField('website',
        searchable = True,
        default = "http://",
        storage = AnnotationStorage(),
        widget = StringWidget(label = _(u'Business Website URL'),
                              description = _(u"Please enter a Website URL."),
                              ),
        ),

    StringField('twitter',
        searchable = True,
        storage = AnnotationStorage(),
        widget = StringWidget(label = _(u'Twitter Name'),
                              description = _(u"Please enter only the Twitter Name. Without '@'"),
                              ),
        ),

    StringField('xing',
        searchable = True,
        storage = AnnotationStorage(),
        widget = StringWidget(label = _(u'Xing URL'),
                              description = _(u"Please enter the complete Xing URL"),
                              ),
        ),

   StringField('language',
        storage = AnnotationStorage(),
        vocabulary = LANGUAGE,
        widget = MultiSelectionWidget(label=_(u"Language"),
                                      description=_(u"In which language will be the talk"),
                                      ),     
        ),
 
    BooleanField(
        name='keynote',
        searchable=True,
        widget=BooleanField._properties['widget'](
            label='Keynote',
            label_msgid='Talk_label_keynote',
            i18n_domain='Talk',
        ),

    ),

    BooleanField(
        name='highlight',
        searchable=True,
        widget=BooleanField._properties['widget'](
            label='Highlight',
            label_msgid='Talk_label_highlight',
            i18n_domain='Talk',
        ),

    ),

    ))

TalkSchema = ATNewsItemSchema.copy() + schema.copy()

TalkSchema['title'].storage = AnnotationStorage()
TalkSchema['description'].storage = AnnotationStorage()
TalkSchema['text'].storage = AnnotationStorage()

finalizeATCTSchema(TalkSchema, folderish=False, moveDiscussion=False)

class Talk(ATNewsItem):
    """Talk
    """

    implements(ITalk)

    portal_type = "Talk"
    _at_rename_after_creation = True

    schema = TalkSchema
    
    security = ClassSecurityInfo()
        
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                return image
        return super(Talk, self).__bobo_traverse__(REQUEST, name)


registerType(Talk, PROJECTNAME)
