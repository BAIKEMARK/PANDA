/**
 * 404 Not Found 页面
 */
import { Result, Button } from 'antd';
import { Link } from 'react-router-dom';

export const NotFoundPage = () => {
  return (
    <Result
      status="404"
      title="404"
      subTitle="抱歉，您访问的页面不存在。"
      extra={
        <Link to="/">
          <Button type="primary" size="large">
            返回首页
          </Button>
        </Link>
      }
    />
  );
};
