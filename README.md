# Hablemos 🗣

Discord bot for Spanish/English servers. Coded in Discordpy

Some key features:

- Suggest conversation topics in Spanish and English


# Commands
- [General](#general)
- [Conversation starters](#conversation-starters)
- [Hangman](#hangman)
- [Quote generator](#Quote-generator)

## General
- **`help`** Shows available commands and further information on their usage
- **`invite`** Invite link to the bot
- **`info`** Information about the bot

## Conversation starters
- **`lst`** Lists available topics
- **`topic <topic>`** Shows a random question from a specified conversation topic. Selects a question from general questions if no topic is specified
    - topics:
        - `general`, `1` - General questions
        - `phil`, `2` - Philosophical questions
        - `would`, `3` - *'Would you rather'* questions
        - `other`,`4` -  Random questions        
        <br>
        [List of questions](https://docs.google.com/spreadsheets/d/10jsNQsSG9mbLZgDoYIdVrbogVSN7eAKbOfCASA5hN0A/edit?usp=sharing)

## Hangman
- `hangman` - runs a new instance of the classic hangman game (but in Spanish)

    For now the only  category is `animales`

## Quote generator
- `quote <message>` or `quote <message_link>` - generates a dramatic looking quote using a user's message

example:

![quote example](https://cdn.discordapp.com/attachments/808679873837137940/920026460234862643/unknown.png)
<br>
# To-Do
- General
    - Add functionality to make prefix configurable
- Conversation starters
    - Add more languages
    - Add ability to show just the requested language
- Hangman
  - add more categories
- Quote generator
  - Use different image style
- Other
    - ~~Spanish Hangman or other vocabulary game~~
    - Reverso contexto
