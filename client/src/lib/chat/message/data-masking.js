import { createWorker } from "tesseract.js"

const MASKED = "**********"
const CREDIT_CARD_NUMBER_PATTERN = /(?:4[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|3[47][0-9]{3}[ -]?[0-9]{6}[ -]?[0-9]{5}|3(?:0[0-5]|[68][0-9])[0-9]{3}[ -]?[0-9]{6}[ -]?[0-9]{4}|6(?:011|5[0-9]{2})[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(?:2131|1800|35\d{3})\d{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4})/
const NRIC_PATTERN = /[STst][0-9]{7}[A-Za-z]/
  

/**
 * 
 * @param {string} message 
 * @returns {Promise<{content: string, messageChanged: boolean}>} Object of the content and changed status
 */
export const cleanSensitiveMessage = async (message) => {
  const ccPattern = new RegExp(CREDIT_CARD_NUMBER_PATTERN, "g")
  const nricPattern = new RegExp(NRIC_PATTERN, "g")

  const cleanedMessage = message.replace(ccPattern, MASKED)
                                .replace(nricPattern, MASKED)   
  const messageChanged = cleanedMessage !== message
  return { content: cleanedMessage, messageChanged }
}

/**
 * 
 * @param {File | Blob | HTMLCanvasElement} image 
 * @returns {Promise<boolean>} result whether is it sensitive
 */
export const detectSensitiveImage = async (image) => {
  const patterns = [CREDIT_CARD_NUMBER_PATTERN, NRIC_PATTERN]

  const upperCaseLetters = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
  const lowerCaseLetters = "ABCDEFGHIJKLMNOPQRSTUVXYZ".toLowerCase()
  const numbers = "0123456789"
  const specialCharacters = "- "
  const whitelistedCharacters = upperCaseLetters + lowerCaseLetters + numbers + specialCharacters

  const ocrWorker = await createWorker()
  await ocrWorker.loadLanguage("eng")
  await ocrWorker.initialize("eng")
  await ocrWorker.setParameters({
    tessedit_char_whitelist: whitelistedCharacters
  })

  const recognizeResults = await ocrWorker.recognize(image)
  const data = recognizeResults.data.text
  console.log(data)
  
  await ocrWorker.terminate()

  const isSensitive = patterns.some((pattern) => {
    return data.match(pattern)
  })
  
  console.log("Sensitive?", isSensitive)
  return isSensitive
}
