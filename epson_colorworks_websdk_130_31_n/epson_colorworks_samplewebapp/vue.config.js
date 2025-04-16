// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

module.exports = {
    pages: {
        index: {
            entry: "src/main.js",
            title: "Web SDK Sample App",
        }
    },
    publicPath: './',
    devServer: {
        proxy: {
            '^/api/': {
                target: 'http://sdk.labelprinter_nw.docker:3000',
                changeOrigin: true
            },
        }
    }
}
