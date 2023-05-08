# Jupiter
> internet relay chat botnet for efnet

## Information
Jupiter will create a botnet by connecting a defined number of clones to every EFNet server. A single host could potentially create over 80 clones without suspicion. It is meant to monitor/jupe/hold nicks & be controlled to do just about anything.

For example, at the time of writing this, there are 14 active EFNet servers. With 3 clones per-server on IPv4 connections, plus another 3 clones per-server on IPv6 connections, thats 6 clones per-server, equating to 84 total clones...all from a single machine. Run this bot on multiple machines, you get the point.

The bot is designed to be very minimal, secure, & trustless by nature. This means anyone can run a copy of your script on their server to help build your botnet.

It is highly recommended that you use a [random spoofing ident protocol daemon](https://github.com/acidvegas/random/blob/master/irc/identd.py)

## Commands
| Command                 | Description                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------------- |
| 5000 \<chan>            | Emulates SuperNETs #5000 channel *(Joins \<chan> and will PM bomb anyone who joins the channel)*   |
| id                      | Send bot identity                                                                                  |
| raw     [-d] \<data>    | Send \<data> to server, optionally delayed with -d argument                                        |
| monitor list            | Return MONITOR list                                                                                |
| monitor reset           | Reset MONITOR list                                                                                 |
| monitor \<+/->\<nicks>  | Add (+) or Remove (-) \<nicks> from MONITOR list. *(Can be a single nick or comma seperated list)* |

**Note:** All commands must be prefixed with @all or the bots nick & will work in a channel or private message.

Raw data must be IRC RFC compliant data & any nicks in the MONITOR list will be juped as soon as they become available.

## Mirrors
- [acid.vegas](https://git.acid.vegas/jupiter)
- [GitHub](https://github.com/acidvegas/jupiter)
- [GitLab](https://gitlab.com/acidvegas/jupiter)
- [SuperNETs](https://git.supernets.org/acidvegas/jupiter)