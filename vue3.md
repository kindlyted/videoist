# Vue3前端技术栈文档

## 项目概述

本项目是一个基于Vue 3的单页面应用程序，使用现代前端技术栈构建。项目采用模块化架构，包含组件、路由、状态管理和API服务等模块。

## 核心技术栈

### 1. Vue 3
- **版本**: Vue 3 Composition API
- **特性**: 使用`<script setup>`语法糖，提供更简洁的组件编写方式
- **状态管理**: Pinia
- **路由管理**: Vue Router

### 2. 构建工具
- **Vite**: 现代化前端构建工具，提供快速的开发服务器和优化的生产构建
- **配置文件**: `vite.config.js`
- **代理配置**: 开发环境下配置了API代理，将`/api`路径代理到`http://localhost:5009`

### 3. CSS框架
- **Tailwind CSS**: 实用优先的CSS框架，用于快速构建自定义设计
- **配置文件**: `tailwind.config.js`
- **PostCSS插件**: 
  - `tailwindcss`: Tailwind CSS插件
  - `autoprefixer`: 自动添加CSS前缀

### 4. HTTP客户端
- **Axios**: 基于Promise的HTTP客户端，用于与后端API通信
- **拦截器**: 
  - 请求拦截器：自动添加JWT Token到请求头
  - 响应拦截器：统一处理响应错误

### 5. 图标库
- **Heroicons**: 为Vue 3优化的高质量SVG图标库
  - 安装方式: `npm install @heroicons/vue`
  - 使用方式: 在组件中导入并使用24px轮廓图标
  - 应用场景: 为按钮、导航菜单等UI元素添加图标以提升用户体验

### 5. 状态管理
- **Pinia**: Vue 3官方推荐的状态管理库
- **特性**: 
  - 使用`defineStore`定义状态存储
  - 支持TypeScript
  - 模块化设计
  - 支持热重载

## 项目结构

```
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── router/
│   ├── services/
│   ├── stores/
│   ├── views/
│   ├── App.vue
│   └── main.js
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 关键配置文件

### 1. package.json
包含项目依赖和脚本命令：
- **依赖包**: vue, vue-router, pinia, axios, tailwindcss等
- **开发依赖**: @vitejs/plugin-vue, autoprefixer等
- **脚本命令**: 
  - `dev`: 启动开发服务器
  - `build`: 构建生产版本
  - `preview`: 预览生产构建

### 2. vite.config.js
Vite配置文件：
- 使用Vue插件
- 配置路径别名`@`指向`src`目录
- 配置API代理

### 3. tailwind.config.js
Tailwind CSS配置文件：
- 配置内容扫描路径
- 扩展主题配置

### 4. main.js
应用入口文件：
- 创建Vue应用实例
- 注册路由和状态管理
- 挂载应用到DOM

## 路由管理

使用Vue Router进行路由管理：
- 路由模式: `createWebHistory`
- 路由守卫: 实现导航守卫控制访问权限
- 路由组件: 每个路由对应一个Vue组件

## 状态管理

使用Pinia进行状态管理：
- 定义用户状态存储(userStore)
- 实现用户登录、注册、登出等功能
- 自动处理JWT Token的存储和清除

## API服务

使用Axios进行HTTP请求：
- 封装API实例
- 自动添加认证Token
- 统一错误处理

## 组件设计

- 使用单文件组件(SFC)
- 采用`<script setup>`语法糖
- 组件化设计，提高代码复用性
- 响应式数据管理
- 图标集成: 在多个组件中集成了Heroicons图标库，提升UI视觉效果
  - DashboardView: 为欢迎标题、信息卡片按钮、导航菜单等添加了图标
  - WordPressManagementView: 为站点管理功能按钮添加了图标
  - WeChatManagementView: 为微信账号管理功能按钮添加了图标
  - VideoCreationView: 为视频创作流程按钮添加了图标

## 样式设计

- 使用Tailwind CSS进行样式设计
- 响应式布局
- 实用类优先的CSS编写方式