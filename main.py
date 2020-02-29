import configargparse
import packt.free_title
import slack.post


def main(args):
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
