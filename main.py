import configargparse
import packt.free_title
import slack.post
import logging
import logging.handlers

LOG_FILENAME = 'learning_alerter.log'
LOG_LEVEL = 'INFO'
LOG_MAX_BYTES = 524288000
LOG_BACKUP_COUNT = 3


def setup_logging():
    logging.basicConfig(level=LOG_LEVEL, filename=LOG_FILENAME, format='%(name)s - %(levelname)s - %(message)s')    
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
    logging.getLogger('root').addHandler(handler)
    return logging.getLogger()


def main(args):
    setup_logging()
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
    args = config.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    main(args)
