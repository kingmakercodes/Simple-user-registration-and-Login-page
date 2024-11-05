import {emailPattern, passwordPattern} from './regexPatterns.js'

// function to validate email format
export function validateEmail(email){
    return emailPattern.test(email);
}

export function validatePassword(password){
    return passwordPattern.test(password)
}