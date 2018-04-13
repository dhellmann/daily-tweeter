import datetime
import logging
import random

from daily_tweeter import posts

import yaml

LOG = logging.getLogger(__name__)


def get_argparse(subparsers):
    schedule_parser = subparsers.add_parser(
        'schedule', help='build a schedule file',
    )
    schedule_parser.add_argument(
        '-f', '--frequency',
        choices=('daily', 'weekly'),
        default='weekly',
        help='how often to schedule posts',
    )
    schedule_parser.add_argument(
        '--shuffle',
        default=False,
        action='store_true',
        help='randomize the post order',
    )
    schedule_parser.add_argument(
        'start_date',
        help='first date to publish, as YYYY-MM-DD',
    )
    schedule_parser.add_argument(
        'post_file',
        help='file containing plain posts',
    )
    schedule_parser.add_argument(
        'schedule_file',
        help='location to write schedule file',
    )
    schedule_parser.set_defaults(
        func=do_schedule,
    )


def do_schedule(args):
    LOG.debug('building schedule for posts from %s', args.post_file)
    post_data = posts.load_posts(args.post_file)
    if not post_data:
        raise RuntimeError('There are no posts in {}'.format(filename))

    if args.shuffle:
        LOG.debug('shuffling posts')
        random.shuffle(post_data)

    if args.frequency == 'daily':
        increment = datetime.timedelta(days=1)
    elif args.frequency == 'weekly':
        increment = datetime.timedelta(days=7)
    else:
        raise ValueError('Unknown --frequency {!r}'.format(args.frequency))

    the_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
    schedule_data = []
    for post in post_data:
        schedule_data.append({
            'date': str(the_date.date()),
            'message': post,
        })
        the_date += increment

    LOG.debug('writing schedule to %s', args.schedule_file)
    with open(args.schedule_file, 'w', encoding='utf-8') as f:
        yaml.dump(
            {'posts': schedule_data},
            f,
            explicit_start=True,
            indent=2,
            default_flow_style=False,
            line_break="\n",
            allow_unicode=True,
        )
