# Hablemos 🗣

Discord bot for Spanish/English servers. Coded in Discordpy

Some key features:

- Suggest conversation topics in Spanish and English


# Commands
- [General](#general)
- [Conversation starters](#conversation-starters)
- [Hangman](#hangman)

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
# To-Do
- General
    - Add command to make prefix configurable
- Conversation starters
    - Add more languages
    - Add ability to show just the requested language
- Other
    - ~~Spanish Hangman or other vocabulary game~~
      - add more categories
    - Reverso contexto
    - Bad jokes