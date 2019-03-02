import StoreMessage from './stores/message/StoreMessage'

export default {
  modules: {
    store__message: StoreMessage
  },
  strict: process.env.NODE_ENV === 'production'
}
