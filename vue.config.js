const path = require('path')
const each = require('lodash/fp/each')

const BundleTrackerPlugin = require('webpack-bundle-tracker')
const CompressionPlugin = require('compression-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin')

class RelativeBundleTrackerPlugin extends BundleTrackerPlugin {
  convertPathChunks (chunks) {
    each(each(chunk => {
      chunk.path = path.relative(this.options.path, chunk.path)
    }))(chunks)
  }

  writeOutput (compiler, contents) {
    if (contents.status === 'done') {
      this.convertPathChunks(contents.chunks)
    }
    super.writeOutput(compiler, contents)
  }
}

const dotenv = require('dotenv')
dotenv.config({
  path: 'lelegis/.env'
})
var HOST_NAME = 'localhost'

module.exports = {
  runtimeCompiler: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/static' : `http://${HOST_NAME}:8080/`,
  outputDir: 'dist',

  chainWebpack: config => {
    config
      .plugin('RelativeBundleTrackerPlugin')
      .use(RelativeBundleTrackerPlugin, [{
        path: '.',
        filename: `./${process.env.DEBUG === 'True' && process.env.NODE_ENV !== 'production' ? 'dev-' : ''}webpack-stats.json`
      }])

    if (process.env.NODE_ENV === 'production') {
      config
        .optimization
        .minimizer('terser')
        .use(TerserPlugin)
        /*
        .tap((args) => {
        args[0].terserOptions.compress.drop_console = true
        args[0].extractComments = true
        args[0].cache = true
        return args
      })
       */

      config
        .plugin('CompressionPlugin')
        .use(CompressionPlugin, [{}])
    } else {
      config
        .devtool('source-map')
    }

    config.module
      .rule('images')
      .use('url-loader')
      .loader('url-loader')
      .tap(options => {
        options.limit = 8192
      })

    // config.resolve.alias
    //  .set('__STATIC__', 'static')

    config.module
      .rule('vue')
      .use('vue-loader')
      .loader('vue-loader')
      .tap(options => {
        options.transformAssetUrls = {
          img: 'src',
          image: 'xlink:href',
          'b-img': 'src',
          'b-img-lazy': ['src', 'blank-src'],
          'b-card': 'img-src',
          'b-card-img': 'img-src',
          'b-carousel-slide': 'img-src',
          'b-embed': 'src'
        }
        return options
      })

    config.devServer
      .public('')
      .port(8080)
      .hot(true)
      .watchOptions({
        poll: true
      })
      .historyApiFallback(true)
      .watchContentBase(true)
      .https(false)
      .headers({
        'Access-Control-Allow-Origin': '*'
      })
      .contentBase([
        path.join(__dirname, 'public'),
        path.join(__dirname, 'src', 'assets')
      ])

    /* config
      .plugin('provide')
      .use(require('webpack/lib/ProvidePlugin'), [{
        $: 'jquery',
        jquery: 'jquery',
        'window.jQuery': 'jquery',
        jQuery: 'jquery',
        _: 'lodash'
      }]) */
  },

  pwa: {
    name: 'LeLegis Analytics',
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      // swSrc is required in InjectManifest mode.
      swSrc: 'public/service-worker.js'
      // ...other Workbox options...
    }
  }
}
