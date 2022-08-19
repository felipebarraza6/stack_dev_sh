import { POST, GET } from './config'


const signup_event = async(data) => {
    
    const request = await POST(`signup_event/`, data)
    return request
  }

const list_participans = async() => {
    const request = await GET('signup_event/')
    return request
}

const get_fingerprint = async(id) => {
  const request = await GET(`profile_footprints/${id}`)
  return request
}

export const callbacks = {
     signupEvent: signup_event,
     list: list_participans,
     fingerprint: {
       retrieve: get_fingerprint
     }
}
