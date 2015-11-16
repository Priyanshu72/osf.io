import sys
import logging

from modularodm import Q

from website.app import init_app
from website.models import DraftRegistration, Sanction, User

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN)
logging.disable(level=logging.INFO)

def main(dry_run=True):
    if dry_run:
        logger.warn('DRY RUN mode')
    pending_approval_drafts = DraftRegistration.find()
    need_approval_drafts = [draft for draft in pending_approval_drafts
                            if draft.requires_approval and draft.approval and draft.approval.state == Sanction.UNAPPROVED]

    for draft in need_approval_drafts:
        sanction = draft.approval
        try:
            if not dry_run:
                sanction.forcibly_reject()
                #manually do the on_reject functionality to prevent send_mail problems
                sanction.meta = {}
                sanction.save()
                draft.approval = None
                draft.save()
            logger.warn('Rejected {0}'.format(draft._id))
        except Exception as e:
            logger.error(e)

if __name__ == '__main__':
    dry_run = 'dry' in sys.argv
    init_app(routes=False)
    main(dry_run=dry_run)
