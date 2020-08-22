import configargparse
import packt.free_title
import slack.post
import logging
import logging.handlers

LOG_MAX_BYTES = 524288000
LOG_BACKUP_COUNT = 3


def setup_logging(args):
    logging.basicConfig(level=args.loglevel, filename=args.logfile, format='%(name)s - %(levelname)s - %(message)s')    
    handler = logging.handlers.RotatingFileHandler(args.logfile, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
    logging.getLogger('root').addHandler(handler)
    return logging.getLogger()


def main(args):
    setup_logging(args)
    if args.packt:
        title, image = packt.free_title.main()
        if args.slacktoken and args.slackchannel:
            token = args.slacktoken
            channel = args.slackchannel
            slack.post.main(token, image, title, channel)
        else:
            print("No args.slacktoken or args.slackchannel found.")
            print("Title is: {}\nImage URL is: {}".format(title, image))


def get_args():
    config = configargparse.ArgParser()
    config.add('--slacktoken')
    config.add('--slackchannel')
    config.add('--packt', action='store_true')
    config.add('--loglevel', default='INFO')
    config.add('--logfile', default='learning_alerter.log')
    args = config.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    main(args)
