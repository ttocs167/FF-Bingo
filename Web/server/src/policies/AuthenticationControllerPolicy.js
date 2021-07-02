const Joi = require('joi')

module.exports = {
    register (req, res, next) {
        const schema = Joi.object({
            email: Joi.string().email(),
            password: Joi.string().regex(/^[a-zA-Z0-9]{8,32}$/)
        })

        const { error } = schema.validate(req.body)

        if (error) {
            switch (error.details[0].context.key) {
                case 'email':
                    res.status(400).send({
                        error: 'You must provide a valid email address.'
                    })
                    break
                case 'password':
                    res.status(400).send({
                        error: `Your password must match the following rules:
                        <br>
                        1. It must contain ONLY the following characters: lower case, upper case, numerics.
                        <br>
                        2. It must be at least 8 characters in length and no more than 32.
                        `
                    })
                    break
                default:
                    res.status(400).send({
                        error: 'Invalid registration information.'
                    })
            }
        } else {
            next()
        }
    }
}
