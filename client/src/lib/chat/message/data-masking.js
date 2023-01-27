import { createWorker } from "tesseract.js"

const MASKED = "**********"
const CREDIT_CARD_NUMBER_PATTERN = /(?:4[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|3[47][0-9]{3}[ -]?[0-9]{6}[ -]?[0-9]{5}|3(?:0[0-5]|[68][0-9])[0-9]{3}[ -]?[0-9]{6}[ -]?[0-9]{4}|6(?:011|5[0-9]{2})[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(?:2131|1800|35\d{3})\d{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4})/
const NRIC_PATTERN = /[STst][0-9]{7}[A-Za-z]/
  

/**
 * Supposedly better clarity for the ocr.
 * But takes forever and does not even help to detect credit card
 * @param {File} image
 * @returns {Promise<File>} File for tesseract
 */
const processImage = async (image) => {
  const imageBitmap = await createImageBitmap(image)
  const canvas = new OffscreenCanvas(imageBitmap.width, imageBitmap.height)
  const ctx = canvas.getContext("2d", { willReadFrequently: true })
  
  ctx.drawImage(imageBitmap, 0, 0)
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
  const { data } = imageData

  //Convert the image to grayscale
  for (let i = 0; i < data.length; i += 4) {
    const avg = (data[i] + data[i + 1] + data[i + 2]) / 3
    data[i] = avg
    data[i + 1] = avg
    data[i + 2] = avg
  }
  ctx.putImageData(imageData, 0, 0)
  
  //Blur the image
  ctx.globalAlpha = 1 / 9;
  ctx.globalCompositeOperation = 'source-over';
  for (let x = 0; x < 3; x++) {
    for (let y = 0; y < 3; y++) {
      ctx.drawImage(canvas, x, y);
    }
  }
  
  //Threshold the image
  const imageDataThresh = ctx.getImageData(0, 0, canvas.width, canvas.height)
  const { data: dataThresh } = imageDataThresh
  const threshold = 128;
  for (let i = 0; i < dataThresh.length; i += 4) {
    const r = dataThresh[i]
    const g = dataThresh[i + 1]
    const b = dataThresh[i + 2]
    const v = (0.2126 * r + 0.7152 * g + 0.0722 * b >= threshold) ? 255 : 0;
    dataThresh[i] = dataThresh[i + 1] = dataThresh[i + 2] = v
  }
  ctx.putImageData(imageDataThresh, 0, 0)

  const processedBlob = await canvas.convertToBlob({ type: image.type })
  const processedImageFile = new File([processedBlob], image.name, {type: image.type})
  return processedImageFile

}

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
 * @param {File} image 
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

  // const processedImage = await processImage(image)

  const data = await (await ocrWorker.recognize(image)).data.text
  console.log(data)
  
  await ocrWorker.terminate()

  const isSensitive = patterns.some((pattern) => {
    return data.match(pattern)
  })
  
  console.log("Sensitive?", isSensitive)
  return isSensitive
}
