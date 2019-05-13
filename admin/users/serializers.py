"""
Serialize user
"""


def serialize_user(user):
    return {
        'username': user.username,
        'name': user.fullname,
        'id': user._id,
        'nodes': list(map(serialize_simple_node, user.contributor_to)),
        #'preprints':list(map(serialize_simple_preprint, user.preprints.all())),
        'emails': user.emails.values_list('address', flat=True),
        'last_login': user.date_last_login,
        'confirmed': user.date_confirmed,
        'registered': user.date_registered,
        'deleted': user.deleted,
        'disabled': user.date_disabled if user.is_disabled else False,
        'two_factor': user.has_addon('twofactor'),
        'osf_link': user.absolute_url,
        'system_tags': user.system_tags,
        'unclaimed': bool(user.unclaimed_records),
        'requested_deactivation': bool(user.requested_deactivation)
    }


def serialize_simple_node(node):
    return {
        'id': node._id,
        'title': node.title,
        'public': node.is_public,
        'number_contributors': len(node.contributors),
        'spam_status': node.spam_status,
        'is_registration': node.is_registration,
        'deleted': node.is_deleted,
    }

def serialize_simple_preprint(preprint):
    return {
        'id': preprint._id,
        'title':preprint.title,
        'description':preprint.description,
        'number_contributors' : len(preprint.contributors),
        'deleted' : preprint.is_deleted,
        'public' : preprint.is_public,
    }
