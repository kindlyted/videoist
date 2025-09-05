// utils/errorHandler.js

/**
 * 获取错误信息键名
 * @param {string} errorCode - 错误码
 * @returns {string} 错误信息键名
 */
export const getErrorMessageKey = (errorCode) => {
  // 如果有错误码，则返回对应的错误信息键名
  if (errorCode) {
    return `errors.${errorCode}`;
  }
  
  // 默认返回未知错误键名
  return 'errors.COMMON_001';
};

/**
 * 处理API错误响应
 * @param {Object} error - 错误对象
 * @returns {Object} 包含错误码和错误信息的对象
 */
export const handleApiError = (error) => {
  // 如果错误对象本身就有错误码（从store返回的情况）
  if (error && error.error_code) {
    return {
      errorCode: error.error_code,
      messageKey: getErrorMessageKey(error.error_code)
    };
  }
  
  // 如果错误响应中有错误码，则使用错误码获取错误信息
  if (error.response && error.response.data && error.response.data.error_code) {
    return {
      errorCode: error.response.data.error_code,
      messageKey: getErrorMessageKey(error.response.data.error_code)
    };
  }
  
  // 如果错误对象本身就有错误信息（从store返回的情况）
  if (error && error.message) {
    return {
      message: error.message
    };
  }
  
  // 如果错误响应中有错误信息，则直接返回
  if (error.response && error.response.data && error.response.data.message) {
    return {
      message: error.response.data.message
    };
  }
  
  // 如果是网络错误
  if (error.code === 'NETWORK_ERROR') {
    return {
      errorCode: 'COMMON_001',
      messageKey: 'errors.COMMON_001'
    };
  }
  
  // 默认返回未知错误
  return {
    errorCode: 'COMMON_001',
    messageKey: 'errors.COMMON_001'
  };
};