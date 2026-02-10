/**
 * 全局动画配置
 * 统一管理应用中的动画效果
 */

// 页面过渡动画
export const pageTransition = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
  transition: { duration: 0.3 }
};

// 淡入动画
export const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  transition: { duration: 0.4 }
};

// 从左滑入
export const slideInLeft = {
  initial: { opacity: 0, x: -20 },
  animate: { opacity: 1, x: 0 },
  transition: { duration: 0.3, ease: 'easeOut' }
};

// 从右滑入
export const slideInRight = {
  initial: { opacity: 0, x: 20 },
  animate: { opacity: 1, x: 0 },
  transition: { duration: 0.3, ease: 'easeOut' }
};

// 从上滑入
export const slideInTop = {
  initial: { opacity: 0, y: -20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.3, ease: 'easeOut' }
};

// 从下滑入
export const slideInBottom = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.3, ease: 'easeOut' }
};

// 缩放动画
export const scaleIn = {
  initial: { opacity: 0, scale: 0.9 },
  animate: { opacity: 1, scale: 1 },
  transition: { duration: 0.3 }
};

// 弹簧缩放
export const springScale = {
  initial: { scale: 0 },
  animate: { scale: 1 },
  transition: { type: 'spring', stiffness: 200, damping: 15 }
};

// 悬停效果
export const hoverScale = {
  whileHover: { scale: 1.05 },
  whileTap: { scale: 0.95 }
};

// 悬停上浮
export const hoverLift = {
  whileHover: { y: -8, transition: { duration: 0.2 } }
};

// 列表项交错动画
export const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.05
    }
  }
};

export const staggerItem = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.3 }
};

// 脉冲动画（用于图标）
export const pulse = {
  animate: {
    scale: [1, 1.1, 1],
    transition: {
      duration: 2,
      repeat: Infinity,
      repeatDelay: 3
    }
  }
};

// 摇摆动画（用于图标）
export const wiggle = {
  animate: {
    rotate: [0, 10, -10, 0],
    transition: {
      duration: 2,
      repeat: Infinity,
      repeatDelay: 3
    }
  }
};

// 渐变背景动画
export const gradientAnimation = {
  animate: {
    backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
    transition: {
      duration: 5,
      repeat: Infinity,
      ease: 'linear'
    }
  }
};
