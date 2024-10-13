const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  // 애플리케이션의 진입점(entry point) 파일 지정
  entry: './src/index.js',

  // 결과물(output)을 어디에 어떻게 저장할지 설정
  output: {
    filename: 'bundle.js', // 번들된 파일 이름
    path: path.resolve(__dirname, 'dist', 'static'), // 빌드된 파일을 저장할 디렉토리
    publicPath: '/static/',
  },
  
  // 모듈과 로더 설정
  module: {
    rules: [
      {
        test: /\.js$/, // .js 파일에 대해 babel-loader를 적용
        exclude: /node_modules/, // node_modules 폴더는 제외
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'] // Make sure these presets are included
          } // ES6+ 코드 변환을 위해 Babel 사용
        },
      },
      
      {
        test: /\.css$/, // .css 파일에 대해 style-loader와 css-loader를 적용
        use: ['style-loader', 'css-loader'],
      },

      {
        test: /\.(png|jpg|gif|svg)$/, // 이미지 파일에 대해 로더 적용
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'images/', // 빌드된 파일이 저장될 폴더
            },
          },
        ],
      },
    ],
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html',
    }),
    new HtmlWebpackPlugin({
      template: './public/news.html', // news.html 템플릿 추가
      filename: 'news.html', // 빌드 후 생성될 파일 이름
    }),
    new HtmlWebpackPlugin({
      template: './public/usertest.html', // usertest.html 템플릿 추가
      filename: 'usertest.html', // 빌드 후 생성될 파일 이름
    }),
    new HtmlWebpackPlugin({
      template: './public/login.html', // usertest.html 템플릿 추가
      filename: 'login.html', // 빌드 후 생성될 파일 이름
    }),
    new HtmlWebpackPlugin({
      template: './public/signup.html', // usertest.html 템플릿 추가
      filename: 'signup.html', // 빌드 후 생성될 파일 이름
    }),
    new CopyWebpackPlugin({
      patterns: [
          { from: 'src/assets/styles', to: '/styles' },  // Copy CSS to dist/static/styles
      ],
    }),
  ],

  devServer: {
    static: './dist',   // dist 폴더를 서빙
    open: true,         // 서버 실행 시 브라우저 자동으로 열림
    hot: true,          // 핫 리로드 (변경 사항 자동 반영)
    port: 3000,         // 서버가 실행될 포트 번호
  },

  // 모드 설정 (development, production)
  mode: 'development', // 개발 모드
};