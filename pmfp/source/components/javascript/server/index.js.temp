import args from "commander"
import init_app from "./application/application"
import {
    init_config
} from './application/config'




function run(options) {
    //console.log(options)
    let config = init_config(options)
    if (options.port) {
        config.set("port", options.port)
    }
    if (options.host) {
        config.set("port", options.host)
    }
    let app = init_app(config)
    if (options.debug) {
        app.run()
    } else {
        app.run(false)
    }
}

function main(argv) {
    args.version('0.0.1')
        .description('run a static http server')
        .option('-P, --port [number]', 'port')
        .option('-H, --host [string]', 'hostname')
        .option('--no-debug', 'use debug mode')
        .option('--config <path>', 'force a config file')
        .parse(argv)
    run(args)
}

if (process.mainModule.filename === __filename) {
    main(process.argv)
}