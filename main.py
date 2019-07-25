import configargparse
import packt.free_title
import slack.post


def main(args):
    if args.packt:
        title, image = packt.free_title.main()
    if args.slacktoken:
        token = args.slacktoken
        channel = args.slackchannel
        slack.post.main(token, image, title, channel)


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
