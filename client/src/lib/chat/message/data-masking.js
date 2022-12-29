const maskSensitiveWord = async (word) => {
  const CREDIT_CARD_NUMBER_PATTERN = /^(?:4[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|3[47][0-9]{3}[ -]?[0-9]{6}[ -]?[0-9]{5}|3(?:0[0-5]|[68][0-9])[0-9]{3}[ -]?[0-9]{6}[ -]?[0-9]{4}|6(?:011|5[0-9]{2})[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(?:2131|1800|35\d{3})\d{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4})$/
  const NRIC_PATTERN = /^[STst][0-9]{7}[A-Za-z]$/

  const masked = "**********"
  
  if (word.match(CREDIT_CARD_NUMBER_PATTERN) || word.match(NRIC_PATTERN)) {
    return word.replace(word, masked)
  }
  
  return word
}

export const cleanSensitiveMessage = async (message) => {
  const words = message.split(" ")

  const cleanedMessageArray = await Promise.all(
    words.map(async word => {
      return await maskSensitiveWord(word)
    })
  )

  const cleanedMessage = cleanedMessageArray.join(" ")
  const messageChanged = cleanedMessage === message

  return {content: cleanedMessage, messageChanged}
}