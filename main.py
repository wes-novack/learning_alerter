import configargparse
import packt.free_title
import slack.post_with_token
import slack.post_with_webhook
import logging
import logging.handlers

LOG_MAX_BYTES = 524288000
LOG_BACKUP_COUNT = 3


def main():
    args = get_args()
    setup_logging(args)
    if args.packt:
        title, image = packt.free_title.main()
        if args.slacktoken and args.slackchannel:
            token = args.slacktoken
            channel = args.slackchannel
            slack.post_with_token.main(token, image, title, channel)
        elif args.slackwebhook:
            webhook = args.slackwebhook
            slack.post_with_webhook.post_to_webhook(webhook, image, title)
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
    args = config.parse_args()
    return args


def setup_logging(args):
    logging.basicConfig(level=args.loglevel, filename=args.logfile, format='%(name)s - %(levelname)s - %(message)s')    
    handler = logging.handlers.RotatingFileHandler(args.logfile, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
    logging.getLogger('root').addHandler(handler)
    return logging.getLogger('root')


if __name__ == '__main__':
    main()
