import logging
import logging.handlers

import configargparse

import packt.free_title
from slack import post_with_token
from slack import post_with_webhook

LOG_MAX_BYTES = 524_288_000
LOG_BACKUP_COUNT = 3


def main():
    args = get_args()
    setup_logging(args)
    if args.packt:
        title, image = packt.free_title.main()
        if args.slacktoken and args.slackchannel:
            token = args.slacktoken
            channel = args.slackchannel
            post_with_token.main(token, image, title, channel)
        elif args.slackwebhook:
            webhook = args.slackwebhook
            post_with_webhook.main(webhook, image, title, args.dryrun)
        else:
            print("Couldn't find (args.slacktoken AND args.slackchannel) or args.slackwebhook.")
            print("Title is: {}\nImage URL is: {}".format(title, image))


def get_args():
    config = configargparse.ArgParser()
    config.add('--slacktoken', env_var='SLACKTOKEN')
    config.add('--slackchannel', env_var='SLACKCHANNEL')
    config.add('--packt', env_var='PACKT', action='store_true')
    config.add('--loglevel', default='INFO')
    config.add('--logfile', default='learning_alerter.log')
    config.add('--slackwebhook', env_var='SLACKWEBHOOK')
    config.add('--dryrun', default=False, action="store_true", env_var="DRYRUN")
    args = config.parse_args()
    return args


def setup_logging(args):
    logging.basicConfig(level=args.loglevel, filename=args.logfile, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    handler = logging.handlers.RotatingFileHandler(args.logfile, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
    #logging.getLogger('root').addHandler(handler)
    return handler #logging.getLogger('root')


if __name__ == '__main__':
    main()
